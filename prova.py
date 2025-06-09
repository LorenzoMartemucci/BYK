import customtkinter
from PIL import Image, ImageTk
import os

class ImageMessageFrame(customtkinter.CTkFrame):
    """
    A custom CustomTkinter frame that displays an image on the left
    and a message on the right.
    """
    def __init__(self, master, image_path, message_text, **kwargs):
        super().__init__(master, **kwargs)

        # Configure the grid for the frame to hold two columns
        # The first column for the image (weight 0 to fit content)
        # The second column for the message (weight 1 to expand)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # --- Image Section (Left) ---
        # Check if the image file exists
        if not os.path.exists(image_path):
            print(f"Warning: Image file not found at '{image_path}'. "
                  "Please provide a valid path. Using a placeholder text for the image.")
            # If image not found, display a placeholder text label
            self.image_label = customtkinter.CTkLabel(self, text="[Image Not Found]", font=("Inter", 12))
        else:
            try:
                # Load the image using PIL (Pillow)
                # Ensure the image is opened in RGB mode to avoid issues with some formats
                pil_image = Image.open(image_path).convert("RGB")

                # Define image dimensions (you can adjust these)
                image_width = 150
                image_height = 150
                pil_image = pil_image.resize((image_width, image_height), Image.Resampling.LANCZOS)

                # Create a CustomTkinter compatible image
                ctk_image = customtkinter.CTkImage(light_image=pil_image,
                                                   dark_image=pil_image,
                                                   size=(image_width, image_height))

                # Create a CTkLabel to display the image
                self.image_label = customtkinter.CTkLabel(self, image=ctk_image, text="") # text="" hides default label text
                self.image_label.image = ctk_image # Keep a reference to prevent garbage collection
            except Exception as e:
                print(f"Error loading image '{image_path}': {e}. Using a placeholder text.")
                self.image_label = customtkinter.CTkLabel(self, text="[Image Load Error]", font=("Inter", 12))

        # Place the image label in the first column, spanning rows (if needed)
        self.image_label.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        # --- Message Section (Right) ---
        # Create a CTkLabel for the message
        self.message_label = customtkinter.CTkLabel(self,
                                                    text=message_text,
                                                    wraplength=300, # Wraps text after 300 pixels
                                                    justify="left", # Aligns text to the left
                                                    font=("Inter", 14)) # Adjust font as needed

        # Place the message label in the second column
        self.message_label.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

class App(customtkinter.CTk):
    """
    Main application class for the CustomTkinter window.
    """
    def __init__(self):
        super().__init__()

        self.title("Image and Message Container")
        self.geometry("600x250") # Set initial window size
        self.resizable(False, False) # Make the window non-resizable for this example

        # Set appearance mode (e.g., "System", "Light", "Dark")
        customtkinter.set_appearance_mode("System")
        # Set default color theme (e.g., "blue", "dark-blue", "green")
        customtkinter.set_default_color_theme("blue")

        # Configure main window grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Example Usage of ImageMessageFrame ---
        # IMPORTANT: Replace "path/to/your/image.png" with the actual path
        # to an image file on your computer for the image to display.
        # Example: image_file = "my_picture.jpg" if it's in the same directory.
        image_file_path = "example_image.png" # <--- !!! CHANGE THIS !!!

        # Create an instance of our custom frame
        self.my_frame = ImageMessageFrame(
            master=self,
            image_path=image_file_path,
            message_text="This is a sample message displayed next to the image. "
                         "It demonstrates how the text wraps within its allocated space "
                         "and aligns to the left."
        )
        # Place the custom frame in the main window
        self.my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()