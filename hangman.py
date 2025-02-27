import streamlit as st
import random
import string
from words import words
from hangman_visual import lives_visual_dict

# Function to get a valid word (without '-' or ' ')
def get_valid_word(words):
    word = random.choice(words)  # randomly chooses something from the list
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()

# Initialize or reset the game state in Streamlit's session_state
if 'word' not in st.session_state:
    st.session_state.word = get_valid_word(words)
    st.session_state.word_letters = set(st.session_state.word)  # letters yet to guess
    st.session_state.used_letters = set()  # letters guessed so far
    st.session_state.lives = 7
    st.session_state.guess = ''

def reset_game():
    st.session_state.word = get_valid_word(words)
    st.session_state.word_letters = set(st.session_state.word)
    st.session_state.used_letters = set()
    st.session_state.lives = 7
    st.session_state.guess = ''

# Title and introduction
st.title("🎭 Hangman Game by ZeeJay 🙅‍♂️")
st.write("📝 Guess the word, one letter at a time!")

# Main game loop (runs every time the app reruns on an interaction)
if st.session_state.lives > 0 and len(st.session_state.word_letters) > 0:
    st.write(f"❤️ You have **{st.session_state.lives}** lives left.")
    st.write("🔠 Used letters: ", ' '.join(sorted(st.session_state.used_letters)))

    # ✅ Fix: Display ASCII Hangman correctly
    st.code(lives_visual_dict[st.session_state.lives], language="plaintext")

    # Show the current state of the word
    word_display = ' '.join([letter if letter in st.session_state.used_letters else '-' for letter in st.session_state.word])
    st.write(f"📖 Current word: **{word_display}**")

    # Input field for the user's guess
    guess = st.text_input("🔡 Guess a letter:", key="guess_input")
    if st.button("🎯 Submit Guess"):
        guess = guess.upper()
        if guess in string.ascii_uppercase and guess not in st.session_state.used_letters:
            st.session_state.used_letters.add(guess)
            if guess in st.session_state.word_letters:
                st.session_state.word_letters.remove(guess)
                st.success(f"✅ Good job! **{guess}** is in the word.")
            else:
                st.session_state.lives -= 1
                st.error(f"❌ Sorry, **{guess}** is not in the word.")
        elif guess in st.session_state.used_letters:
            st.warning("⚠️ You already guessed that letter. Try another!")
        else:
            st.warning("🚨 Please enter a valid letter (A-Z).")

# When lives run out
elif st.session_state.lives == 0:
    st.code(lives_visual_dict[st.session_state.lives], language="plaintext")
    st.error(f"💀 You lost! The word was **{st.session_state.word}**.")
    if st.button("🔄 Restart Game"):
        reset_game()

# When the user wins
else:
    st.balloons()  # simple celebratory animation!
    st.success(f"🎉 Congratulations! You guessed the word **{st.session_state.word}**! 🎊")
    if st.button("🔄 Play Again"):
        reset_game()
