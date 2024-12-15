import outetts
import torch

# Configure the model
model_config = outetts.GGUFModelConfig_v1(
    model_path="model/OuteTTS-0.2-500M-FP16.gguf",
    language="en", # Supported languages in v0.2: en, zh, ja, ko
    dtype=torch.bfloat16,
    additional_model_config={
        'attn_implementation': "flash_attention_2"
    }
)

# Initialize the GGUF interface
interface = outetts.InterfaceGGUF(model_version="0.2", cfg=model_config)

# Optional: Create a speaker profile (use a 10-15 second audio clip)
# speaker = interface.create_speaker(
#     audio_path="path/to/audio/file",
#     transcript="Transcription of the audio file."
# )

# Optional: Save and load speaker profiles
# interface.save_speaker(speaker, "speaker.json")
speaker = interface.load_speaker("D:\Diffusion_Auto_F111\OuteTTS\speakers\WomanClear1.json")

# Optional: Load speaker from default presets
#interface.print_default_speakers()
#speaker = interface.load_default_speaker(name="male_1")

output = interface.generate(
    text="Speech synthesis is the artificial production of human speech. A computer system used for this purpose is called a speech synthesizer, and it can be implemented in software or hardware products.",
    # Lower temperature values may result in a more stable tone,
    # while higher values can introduce varied and expressive speech
    temperature=0.1,
    repetition_penalty=1.0,
    max_length=4096,

    # Optional: Use a speaker profile for consistent voice characteristics
    # Without a speaker profile, the model will generate a voice with random characteristics
    speaker=speaker,
)

# Save the synthesized speech to a file
output.save("output.wav")

# Optional: Play the synthesized speech
# output.play()
