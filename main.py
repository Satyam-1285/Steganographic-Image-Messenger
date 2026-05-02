from PIL import Image
import binascii

class GhostCode:
    def __init__(self):
        self.header = "GHOST" # Identifier to check for hidden messages

    def _text_to_bin(self, text):
        # Converts text to a binary string
        return bin(int(binascii.hexlify(text.encode()), 16))[2:].zfill(8 * len(text))

    def _bin_to_text(self, binary):
        # Converts binary string back to text
        hex_data = hex(int(binary, 2))[2:]
        return binascii.unhexlify(hex_data).decode()

    def encode(self, image_path, secret_message, output_path):
        img = Image.open(image_path)
        encoded_msg = self.header + secret_message + "###" # '###' is the EOF marker
        binary_msg = self._text_to_bin(encoded_msg)
        
        pixels = list(img.getdata())
        new_pixels = []
        bit_idx = 0

        for pixel in pixels:
            if bit_idx < len(binary_msg):
                # Modify the Least Significant Bit (LSB) of the Red channel
                new_red = (pixel[0] & ~1) | int(binary_msg[bit_idx])
                new_pixels.append((new_red, pixel[1], pixel[2]))
                bit_idx += 1
            else:
                new_pixels.append(pixel)

        img.putdata(new_pixels)
        img.save(output_path, "PNG")
        print(f"Successfully haunted {output_path} with your secret.")

    def decode(self, image_path):
        img = Image.open(image_path)
        pixels = list(img.getdata())
        
        binary_msg = ""
        for pixel in pixels:
            binary_msg += str(pixel[0] & 1)

        # Split binary into 8-bit chunks and convert to chars
        all_text = ""
        for i in range(0, len(binary_msg), 8):
            byte = binary_msg[i:i+8]
            try:
                char = chr(int(byte, 2))
                all_text += char
                if "###" in all_text: break
            except: break

        if all_text.startswith(self.header):
            return all_text.replace(self.header, "").replace("###", "")
        return "No ghost found in this image."

# --- QUICK TEST ---
if __name__ == "__main__":
    ghost = GhostCode()
    
    # Usage:
    # 1. Place a file named 'input.png' in the folder
    # 2. ghost.encode("input.png", "The meeting is at midnight.", "haunted.png")
    # 3. print(ghost.decode("haunted.png"))
    
    print("GhostCode initialized. Use .encode() and .decode() to hide messages in PNGs.")
