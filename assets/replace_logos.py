from PIL import Image
import os

# Define the path to your logo and target icon paths
logo_path = r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\logo.png"  # Update this with your actual logo path
icons = [
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\android-icon-36x36.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\android-icon-48x48.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\android-icon-72x72.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\android-icon-96x96.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\android-icon-144x144.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\android-icon-192x192.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-57x57.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-60x60.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-72x72.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-76x76.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-114x114.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-120x120.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-144x144.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-152x152.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\apple-icon-180x180.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\favicon-16x16.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\favicon-32x32.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\favicon-96x96.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\ms-icon-70x70.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\ms-icon-144x144.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\ms-icon-150x150.png",
    r"C:\Users\adunw\OneDrive\Documents\GitHub\atdunwoody.github.io\assets\icons\ms-icon-310x310.png",
]

# Open the logo
logo = Image.open(logo_path)

# Function to resize the logo and overwrite the existing icon
def replace_icon(icon_path):
    # Extract size from the filename, removing the extension first
    filename = os.path.basename(icon_path)
    size_str = filename.split('-')[-1].split('.')[0]  # Get the part with dimensions, removing the extension
    size = tuple(map(int, size_str.split('x')))  # Split the size string and convert to a tuple of integers
    
    # Resize the logo to the desired size
    resized_logo = logo.resize(size, Image.Resampling.LANCZOS)
    
    # Save the resized logo to replace the icon
    resized_logo.save(icon_path)

# Replace each icon with the resized logo
for icon in icons:
    replace_icon(icon)

print("Icons replaced successfully!")
