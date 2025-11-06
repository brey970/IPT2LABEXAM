import mysql.connector
import re

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="resume_db"
    )

def validate_email(email):
    return "@" in email and "." in email

def validate_phone(phone):
    return re.match(r"^\(\d{3}\) \d{3}-\d{4}$", phone)

def add_resume():
    conn = connect_db()
    cursor = conn.cursor()

    print("\n=== Add New Resume ===")
    full_name = input("Full Name: ")
    age = int(input("Age (18–70): "))
    address = input("Address: ")
    phone = input("Phone ((XXX) XXX-XXXX): ")
    email = input("Email: ")
    job_title = input("Job Title: ")
    summary = input("Professional Summary (optional): ")

    if not (full_name and address and job_title):
        print("Required fields missing.")
        return
        
    if not (18 <= age <= 70):
        print("Invalid age.")
        return
        
    if not validate_phone(phone):
        print("Invalid phone format.")
        return
        
    if not validate_email(email):
        print("Invalid email.")
        return

    cursor.execute("""
        INSERT INTO resumes (full_name, age, address, phone, email, job_title, summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (full_name, age, address, phone, email, job_title, summary))
    resume_id = cursor.lastrowid

    print("\nEnter Experience (leave job title blank to stop):")
    while True:
        job = input("Job Title: ")
        if not job: break
        company = input("Company: ")
        years = input("Years: ")
        cursor.execute("INSERT INTO experience (resume_id, job_title, company, years) VALUES (%s, %s, %s, %s)",
                       (resume_id, job, company, years))


    
    print("\nEnter Education (leave degree blank to stop):")
    while True:
        degree = input("Degree: ")
        if not degree: break
        institution = input("Institution: ")
        year = input("Year: ")
        cursor.execute("INSERT INTO education (resume_id, degree, institution, year) VALUES (%s, %s, %s, %s)",
                       (resume_id, degree, institution, year))

    skills = input("Skills (comma-separated): ").split(",")
    for skill in skills:
        cursor.execute("INSERT INTO skills (resume_id, skill) VALUES (%s, %s)", (resume_id, skill.strip()))



    

    conn.commit()
    cursor.close()
    conn.close()
    print("Resume saved successfully!")

def view_resumes():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resumes")
    resumes = cursor.fetchall()

    for r in resumes:
        print("\n==============================")
        print(f"{r['full_name']} | {r['job_title']}")
        print(f"{r['phone']} | {r['email']}")
        print(f"{r['address']}")
        if r['summary']:
            print(f"\nSummary:\n{r['summary']}")

        cursor.execute("SELECT * FROM experience WHERE resume_id = %s", (r['id'],))
        for e in cursor.fetchall():
            print(f"- {e['job_title']} at {e['company']} ({e['years']})")

        cursor.execute("SELECT * FROM education WHERE resume_id = %s", (r['id'],))
        for e in cursor.fetchall():
            print(f"- {e['degree']}, {e['institution']} ({e['year']})")

        cursor.execute("SELECT skill FROM skills WHERE resume_id = %s", (r['id'],))
        skills = [s['skill'] for s in cursor.fetchall()]
        print("\nSkills:")
        print(", ".join(skills))
        print("==============================")

    cursor.close()
    conn.close()

def main():
    while True:
        print("\n=== Resume Builder ===")
        print("1. Add New Resume")
        print("2. View All Resumes")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            add_resume()
        elif choice == '2':
            view_resumes()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":

    main()

