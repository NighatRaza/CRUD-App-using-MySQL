import mysql.connector
import streamlit as st

# Function to establish a connection to MySQL Server
def init_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

# Initialize the connection
mydb = init_connection()
mycursor = mydb.cursor()
# print("Connection Established")
st.write("Connection Established")

# Function to reset the auto-increment value
def reset_auto_increment():
    mycursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
    mydb.commit()

# Create Streamlit App

def main():
    st.title("CRUD Operations With MySQL");

    # Display Options for CRUD Operations
    option=st.sidebar.selectbox("Select an Operation",("Create","Read","Update","Delete"))
    # Perform Selected CRUD Operations
    if option=="Create":
        st.subheader("Create a Record")
        name=st.text_input("Enter Name")
        email=st.text_input("Enter Email")
        if st.button("Create"):
            sql= "insert into users(name,email) values(%s,%s)"
            val= (name,email)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Created Successfully!!!")



    elif option=="Read":
        st.subheader("Read Records")
        mycursor.execute("select * from users")
        result = mycursor.fetchall()
        for row in result:
            st.write(row)



    elif option=="Update":
        st.subheader("Update a Record")
        id=st.number_input("Enter ID",min_value=1)
        name=st.text_input("Enter New Name")
        email=st.text_input("Enter New Email")
        if st.button("Update"):
            sql="update users set name=%s, email=%s where id =%s"
            val=(name,email,id)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Updated Successfully!!!")




    elif option=="Delete":
        st.subheader("Delete a Record")
        id=st.number_input("Enter ID",min_value=1)
        if st.button("Delete"):
            sql="delete from users where id =%s"
            val=(id,)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Record Deleted Successfully!!!")

            # Check if the table is empty
            mycursor.execute("SELECT COUNT(*) FROM users")
            count = mycursor.fetchone()[0]
            if count == 0:
                reset_auto_increment()
                st.info("All records deleted.")
#

if __name__ == "__main__":
    main()







