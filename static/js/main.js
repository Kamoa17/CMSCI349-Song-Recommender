/**
 * Add a song to the user's collection of liked song (i.e, their song library)
 * @param {string} songId - The unique ID of the song
 */
const AddSongToLikedSongs = async (songId) => {
    try {
        const response = await fetch(`/api/song/metadata/add/${songId}`, { method: "POST" });
        response.json().then(res => {
            let toast = new Snacky({ actionButton: true, actionText: "Dismiss" })
            if (res.response == 200) {
                toast.show("Song added to your library")
            }
            else {
                toast.show("An error occurred")
            }
        })
    }
    catch (err) {
        throw new Error(err)
    }
}

/**
 * Attach the like event listener to the like button
 */
const LikeEventListener = () => {
    const likeButtons = document.querySelectorAll(".like-button")
    likeButtons.forEach(likeButton => {
        const songId = likeButton.getAttribute("data-song-id")
        likeButton.addEventListener("click", () => {
            AddSongToLikedSongs(songId)
        })
    })
}

// Attach the event listeners after the DOM is loaded and parsed
document.addEventListener("DOMContentLoaded", LikeEventListener)