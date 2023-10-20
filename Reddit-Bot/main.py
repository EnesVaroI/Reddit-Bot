from auth import authenticate
from bot_logic import run_bot

if __name__ == "__main__":
    reddit = authenticate()
    run_bot(reddit)
