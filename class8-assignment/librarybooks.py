import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel

class LibraryBook(BaseModel):
    book_id: int | str
    book_title: str
    author_name: str
    is_available: bool

library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True
)

@function_tool
def get_book_info(wrapper: RunContextWrapper[LibraryBook]):
    return f'The Library Book is {wrapper.context}'

personal_agent = Agent(
    name = "Agent",
    instructions="You are a helpful assistant, always call the tool to get library's book information",
    tools=[get_book_info]
)

async def main():
    result = await Runner.run(
        personal_agent,  
        'tell me library book information', 
        run_config=config,
        context = library_book
        )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())