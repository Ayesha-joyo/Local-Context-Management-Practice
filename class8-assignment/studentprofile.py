import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel

class StudentProfile(BaseModel):
    student_id: int | str
    student_name: str
    current_semester: int
    total_courses: int 

student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

@function_tool
def get_student_info(wrapper: RunContextWrapper[StudentProfile]):
    return f'The Student Profile is {wrapper.context}'

personal_agent = Agent(
    name = "Agent",
    instructions="You are a helpful assistant, always call the tool to get student's information",
    tools=[get_student_info]
)

async def main():
    result = await Runner.run(
        personal_agent,  
        'What is student id and also tell me his current semester', 
        run_config=config,
        context = student
        )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())