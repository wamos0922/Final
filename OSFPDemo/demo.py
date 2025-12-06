import os
from PIL import Image

# Import from installed ossimg library
try:
    from ossimg import (
        load_image,
        apply_golden_hour,
        apply_gritty_contrast,
        apply_pastel_matte,
        process_manual_edits
    )
except ImportError as e:
    print("=" * 70)
    print("  ERROR: ossimg library is not installed!")
    print("=" * 70)
    print("\nPlease install the library first:")
    print("\n  Method 1 - From GitHub (Recommended):")
    print("  pip install git+https://github.com/wamos0922/OSFinalProjectLibrary.git")
    print("\n  Method 2 - For Development:")
    print("  git clone https://github.com/wamos0922/OSFinalProjectLibrary.git")
    print("  cd OSFinalProjectLibrary")
    print("  pip install -e .")
    print("\n" + "=" * 70)
    exit(1)


def get_float_input(prompt: str, default_value: float) -> float:
    while True:
        try:
            user_input = input(f"{prompt} (Default: {default_value:.2f}): ").strip()
            if not user_input:
                return default_value
            return float(user_input)
        except ValueError:
            print(" Invalid input. Please enter a number.")


def create_dummy_image(filename="images/sample_input.png"):
    os.makedirs("images", exist_ok=True)
    
    if not os.path.exists(filename):
        print(f"📷 Creating dummy image: {filename}")
        img = Image.new('RGB', (400, 300), color='#6A5ACD')
        img.save(filename)
        print(f"✅ Created: {filename}")


def run_manual_edit(img: Image.Image) -> Image.Image:
    print("\n" + "=" * 70)
    print(" " * 15 + "MANUAL EDIT MODE")
    print("=" * 70)
    print("\nYou'll be asked to configure 4 parameters.")
    print("Press Enter to use default values.\n")
    
    # Collect all inputs first
    print("-" * 70)
    print("[1/4] SATURATION")
    print("  • 1.0 = original")
    print("  • 0.0 = grayscale")
    print("  • >1.0 = more vibrant")
    print("-" * 70)
    saturation_factor = get_float_input("Enter Saturation Factor", 1.0)
    
    print("\n" + "-" * 70)
    print("[2/4] SHADOWS")
    print("  • 0.0 = neutral")
    print("  • Positive = lift shadows (brighter)")
    print("  • Negative = crush shadows (darker)")
    print("-" * 70)
    shadows_amount = get_float_input("Enter Shadows Amount", 0.0)
    
    print("\n" + "-" * 70)
    print("[3/4] BRIGHTNESS")
    print("  • 1.0 = original")
    print("  • >1.0 = brighter")
    print("  • <1.0 = darker")
    print("-" * 70)
    brightness_factor = get_float_input("Enter Brightness Factor", 1.0)
    
    print("\n" + "-" * 70)
    print("[4/4] SHARPNESS")
    print("  • 1.0 = original")
    print("  • >1.0 = sharper")
    print("  • <1.0 = blurrier")
    print("-" * 70)
    sharpness_factor = get_float_input("Enter Sharpness Factor", 1.0)
    
    # Ensure output directory exists
    os.makedirs("outputs", exist_ok=True)
    
    # Apply edits step-by-step
    print("\n" + "=" * 70)
    print("Applying Edits Step-by-Step...")
    print("=" * 70)
    
    edit_sequence = process_manual_edits(
        img,
        saturation_factor,
        shadows_amount,
        brightness_factor,
        sharpness_factor
    )
    
    final_img = None
    step_count = 1
    
    for feature_name, current_img in edit_sequence:
        preview_name = f"outputs/preview_{step_count:02d}_{feature_name}.png"
        current_img.save(preview_name)
        print(f"  📸 Step {step_count}: {feature_name.upper():12} → {preview_name}")
        final_img = current_img
        step_count += 1
    
    # Save final result
    if final_img:
        final_name = "outputs/output_FINAL_MANUAL_EDIT.png"
        final_img.save(final_name)
        print(f"\n🎉 Final combined result: {final_name}")
        return final_img
    
    return img


def main():
    INPUT_FILE = "images/sample_input.png"
    
    # Ensure directories exist
    os.makedirs("images", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    
    # Create sample image if needed
    create_dummy_image(INPUT_FILE)
    
    # Check if input exists
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: Input file '{INPUT_FILE}' is missing.")
        print("Please place an image at 'images/sample_input.png'")
        return
    
    try:
        # Load original image
        original_img = load_image(INPUT_FILE)
        
        # Display menu
        print("\n" + "=" * 70)
        print(" " * 20 + "ossimg Library Demo")
        print("=" * 70)
        print("\nChoose an option:\n")
        print("  1: Apply 'Golden Hour' Template")
        print("     └─ Warm, soft aesthetic with lifted shadows\n")
        print("  2: Apply 'Gritty Contrast' Template")
        print("     └─ Urban, high-contrast look with deep shadows\n")
        print("  3: Apply 'Pastel Matte' Template")
        print("     └─ Soft, faded, dreamy appearance\n")
        print("  4: Manual Edit Mode")
        print("     └─ Customize all 4 parameters yourself\n")
        print("=" * 70)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        final_img = None
        output_suffix = None
        
        # Process based on choice
        if choice == '1':
            print("\n Applying: Golden Hour Template...")
            final_img = apply_golden_hour(original_img)
            output_suffix = "GOLDEN_HOUR"
            
        elif choice == '2':
            print("\n Applying: Gritty Contrast Template...")
            final_img = apply_gritty_contrast(original_img)
            output_suffix = "GRITTY_CONTRAST"
            
        elif choice == '3':
            print("\n Applying: Pastel Matte Template...")
            final_img = apply_pastel_matte(original_img)
            output_suffix = "PASTEL_MATTE"
            
        elif choice == '4':
            final_img = run_manual_edit(original_img)
            output_suffix = None  # Already saved in run_manual_edit()
            
        else:
            print("\n Invalid choice. Please enter a number between 1-4.")
            return
        
        # Save template results
        if final_img and output_suffix:
            output_name = f"outputs/output_FINAL_{output_suffix}.png"
            final_img.save(output_name)
            print(f"\n Success! Saved as: {output_name}")
        
        print("\n" + "=" * 70)
        print("Demo completed! Check the 'outputs/' folder for results.")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n Error during processing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()