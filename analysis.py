# file2.py

import requests
import json
import test  # Import file1 instead of test
from plyer import notification
import tkinter as tk
from tkinter import scrolledtext, ttk
import time

def send_prompt(content):
    url = "http://localhost:11434/api/chat"

    data = {
        "model": "llama3.2",
        "messages": [
            {
                "role": "user",
                "content": f"Write counter-measures for this cyber attack in 5-10 points. After this sentence if you find '--' character sequence, simply write 'No danger detected' : {content}"
            },
        ],
        "stream": True
    }

    response = requests.post(url, json=data, stream=True)
    if response.status_code == 200:
        full_response = ''
        for line in response.iter_lines():
            if line:
                try:
                    json_object = json.loads(line)
                    if 'message' in json_object and 'content' in json_object['message']:
                        chunk = json_object['message']['content']
                        full_response += chunk
                except json.JSONDecodeError:
                    pass
        print()
        return full_response
    else:
        print(f"Error: {response.status_code}")
        return response.text

def show_countermeasures_in_window(countermeasures):
    """Opens a styled Tkinter window with countermeasures displayed."""

    # Create and configure the main window
    window = tk.Tk()
    window.title("Countermeasures for Detected Attack")
    window.geometry("700x500")
    window.configure(bg="#2b2b2b")  # Dark background for a modern look

    # Title label
    title_label = tk.Label(
        window,
        text="Recommended Countermeasures",
        font=("Helvetica", 16, "bold"),
        fg="white",
        bg="#2b2b2b"
    )
    title_label.pack(pady=(20, 10))

    # Separator
    separator = ttk.Separator(window, orient="horizontal")
    separator.pack(fill="x", padx=20, pady=(0, 15))

    # Styled text area for the countermeasures
    frame = tk.Frame(window, bg="#2b2b2b")
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    text_area = scrolledtext.ScrolledText(
        frame,
        wrap=tk.WORD,
        width=80,
        height=20,
        font=("Helvetica", 12),
        fg="#e0e0e0",
        bg="#1e1e1e",
        insertbackground="white",
        selectbackground="#505050"
    )
    text_area.pack(fill="both", expand=True)
    text_area.insert(tk.END, countermeasures)
    text_area.configure(state="disabled")  # Make text read-only

    # Close button
    close_button = tk.Button(
        window,
        text="Close",
        font=("Helvetica", 12, "bold"),
        fg="white",
        bg="#4caf50",
        activebackground="#388e3c",
        activeforeground="white",
        command=window.destroy
    )
    close_button.pack(pady=20)

    # Run the main event loop
    window.mainloop()

def notify_user(attack_type, countermeasures):
    """Displays a notification and adds a clickable button for the user to view countermeasures."""
    notification.notify(
        title="Security Alert",
        message=f"There could be a possible threat of {attack_type}. Click here to learn about the counter-measures.",
        timeout=5,
        app_name="Security Monitor"
    )

    # After notification, ask the user to press Enter to view countermeasures
    user_input = input("Press Enter to view countermeasures...")

    if user_input == "":
        show_countermeasures_in_window(countermeasures)

def main():
    # Get the attack result from file1
    content = test.get_attack_result()

    # Only proceed if there's an attack (not '--')
    if content and content != '--':
        countermeasures = send_prompt(content)

        # Show notification and simulate click by prompting user to view countermeasures
        notify_user(content, countermeasures)
    else:
        print("No danger detected.")

if __name__ == "__main__":
    main()