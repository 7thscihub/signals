import traceback
from scripts.scalper import scalper, scalper_debugger


def main():
    scalper()
    
        
if __name__ == "__main__":
    print("Mooneazy running...")
    try:
        main()
    except Exception as e:
        # traceback.print_exc()
        # input("\n Press Enter to Close Window")
        raise e
    