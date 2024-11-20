import random
from num2words import num2words
from datetime import datetime
import io
import asyncio
from pydub import AudioSegment
import concurrent.futures
import edge_tts

def generate_french_number(min_val=10, max_val=99):
    return random.randint(min_val, max_val)

def generate_four_digit_number():
    return random.randint(1000, 2050)

def number_to_french(number):
    return num2words(number, lang='fr')

def generate_phone_number():
    return [random.randint(10, 99) for _ in range(5)]

def generate_price_sentence():
    sentences = [
        ("Cette chemise coûte {} euros {}", (random.randint(5, 100), random.randint(10, 99))),
        ("Le livre coûte {} euros {}", (random.randint(5, 50), random.randint(10, 99))),
        ("Le château est construit en {}", (random.randint(1100, 1500),)),
        ("Il y a {} personnes dans la salle", (random.randint(10, 150),)),
        ("Le train part à {} heures {}", (random.randint(0, 23), random.randint(10, 59))),
        ("La température est de {} degrés", (random.randint(-5, 35),)),
        ("L'appartement fait {} mètres carrés", (random.randint(30, 150),))
    ]
    template, numbers = random.choice(sentences)
    return template.format(*numbers), numbers

def text_to_speech(text):
    """
    Converts text to speech using edge-tts and returns an AudioSegment.
    """
    async def get_audio():
        communicate = edge_tts.Communicate(text, "fr-CA-ThierryNeural")
        buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buffer.write(chunk["data"])
        buffer.seek(0)
        return AudioSegment.from_mp3(buffer)

    return asyncio.run(get_audio())

def process_number(number):
    french_text = number_to_french(number)
    return text_to_speech(french_text)

def main():
    # Generate numbers
    two_digit_numbers = [generate_french_number() for _ in range(10)]
    four_digit_numbers = [generate_four_digit_number() for _ in range(10)]
    phone_numbers = [generate_phone_number() for _ in range(10)]
    sentences = [generate_price_sentence() for _ in range(5)]

    # Convert numbers to French words
    french_two_digit = [number_to_french(num) for num in two_digit_numbers]
    french_four_digit = [number_to_french(num) for num in four_digit_numbers]

    # Create audio segments
    audio_segments = []
    
    # Function to add section with silence
    def add_section(items_to_process, processor, silence_duration=1500):
        # Add 3 seconds of silence at the start
        audio_segments.append(AudioSegment.silent(duration=3000))
        
        # Process items in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            audio_parts = list(executor.map(processor, items_to_process))
        
        # Add items with silence intervals
        for audio in audio_parts:
            audio_segments.append(audio)
            audio_segments.append(AudioSegment.silent(duration=silence_duration))

    # Add two-digit numbers
    add_section(french_two_digit, text_to_speech)

    # Add four-digit numbers
    add_section(french_four_digit, text_to_speech)

    # Add phone numbers with proper intervals
    audio_segments.append(AudioSegment.silent(duration=3000))  # 3s silence before phone numbers
    
    # Process each phone number set
    for phone_set in phone_numbers:
        # Process each number in the set
        for i, num in enumerate(phone_set):
            # Add the number
            audio_segments.append(text_to_speech(number_to_french(num)))
            # Add 0.3s silence between numbers within a set, or 1s after the last number of the set
            if i < len(phone_set) - 1:
                audio_segments.append(AudioSegment.silent(duration=300))  # 0.3s between numbers in set
            else:
                audio_segments.append(AudioSegment.silent(duration=1000))  # 1s between sets

    # Add sentences
    add_section([sentence for sentence, _ in sentences], text_to_speech)

    # Combine all audio segments
    final_audio = sum(audio_segments)

    # Export the final audio
    final_audio.export("french_numbers_dictation.mp3", format="mp3")

    # Generate log file
    log_filename = f"{datetime.now().strftime('%Y%m%d')}_numbers_log.txt"
    with open(log_filename, "w", encoding='utf-8') as log_file:
        log_file.write("Audio file 'french_numbers_dictation.mp3' has been created.\n\n")
        
        log_file.write("Two-digit numbers:\n")
        for i, num in enumerate(two_digit_numbers, 1):
            log_file.write(f"{i}. {num} ({number_to_french(num)})\n")
        
        log_file.write("\nFour-digit numbers:\n")
        for i, num in enumerate(four_digit_numbers, 1):
            log_file.write(f"{i}. {num} ({number_to_french(num)})\n")
        
        log_file.write("\nPhone numbers:\n")
        for i, phone_set in enumerate(phone_numbers, 1):
            log_file.write(f"{i}. {'-'.join(str(num).zfill(2) for num in phone_set)}\n")
        
        log_file.write("\nSentences:\n")
        for i, (sentence, _) in enumerate(sentences, 1):
            log_file.write(f"{i}. {sentence}\n")

    print(f"Log file '{log_filename}' has been created.")

if __name__ == "__main__":
    main()
