from agents import resume_agent

TEST_RESUME = """
Meghana Adithi
Software Engineer with experience in Python, React, and cloud platforms.
Worked on backend services, APIs, and data-driven applications.

Skills: Python, JavaScript, React, FastAPI, SQL
Tools: AWS, Git, Docker
Experience: 2 years
"""

if __name__ == "__main__":
    result = resume_agent(TEST_RESUME)
    print("=== Resume Agent Output ===")
    print(result)

