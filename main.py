from live import run_live
from video import run_video

print("1. Live Camera")
print("2. Video File")

choice = input("Enter choice: ")

if choice == "1":
    run_live()
elif choice == "2":
    run_video()
else:
    print("Invalid choice")