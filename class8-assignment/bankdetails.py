import asyncio
from connection import config
from agents import Agent, RunContextWrapper, Runner, function_tool
from pydantic import BaseModel

class BankAccount(BaseModel):
    account_number: int | str
    customer_name: str
    account_balance: float
    account_type: int | str

bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500.50,
    account_type="savings"
)

@function_tool
def get_bank_info(wrapper: RunContextWrapper[BankAccount]):
    return f'The Bank Account is {wrapper.context}'

personal_agent = Agent(
    name = "Agent",
    instructions="You are a helpful assistant, always call the tool to get bank account's information",
    tools=[get_bank_info]
)

async def main():
    result = await Runner.run(
        personal_agent,  
        'What is account balance and also tell me account type', 
        run_config=config,
        context = bank_account 
        )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())