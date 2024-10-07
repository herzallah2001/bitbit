import os
import hashlib

# Define piece size (e.g., 512 KB)
PIECE_SIZE = 512 * 1024  # 512 KB in bytes

def divide_file_and_generate_hashes(file_path, output_dir):
    """
    Divides a file into smaller pieces, generates SHA1 hash for each piece,
    names each piece by its hash, and concatenates all the hashes.
    
    :param file_path: Path to the original file.
    :param output_dir: Directory to store the pieces.
    :return: A concatenated string of all the piece hashes.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the file size
    file_size = os.path.getsize(file_path)
    
    # Calculate the number of pieces needed
    num_pieces = (file_size + PIECE_SIZE - 1) // PIECE_SIZE  # Ceiling division
    all_piece_hashes = b''  # Concatenated hashes

    with open(file_path, 'rb') as f:
        for i in range(num_pieces):
            piece_data = f.read(PIECE_SIZE)  # Read the piece
            
            # Generate SHA1 hash for the piece and use it as the filename
            piece_hash = hashlib.sha1(piece_data).digest()
            piece_hash_hex = piece_hash.hex()  # Convert hash to hex
            piece_filename = os.path.join(output_dir, f'{piece_hash_hex}')  # Name the piece by its hash

            # Write the piece to a new file named by its hash
            with open(piece_filename, 'wb') as piece_file:
                piece_file.write(piece_data)
                
            all_piece_hashes += piece_hash  # Concatenate the piece hash

            print(f"Piece {i + 1} saved as: {piece_filename}, Hash: {piece_hash_hex}")

    print(f"File divided into {num_pieces} pieces.")
    
    return all_piece_hashes


