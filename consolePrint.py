from datetime import datetime

async def console_print(print_type: str, tail_print: str):
    print(f"{datetime.now().strftime('%H:%M:%S%p')} | [{print_type.upper()}] | {tail_print}")
