/**
 * Update the home page with recommendations returned from the API
 * 
 * @param {Array<JSON>} recommendations A list of recommended songs returned from the API
 */

const UpdatePage = (recommendations) => {
    let recommendationsContainer = document.querySelector("#recommendations-container");
    let recommendationsContent = ""

    // for each recommendation, build a recommendation list item
    for (let recommendation of recommendations) {
        let recItem = `
            <li class="grid__item">
                <span class="material-icons like-button"
                    data-song-id="${recommendation['track_id']}">thumb_up</span>
                <a class="grid__link" href="${recommendation['track_url']}">
                    <div class="img-wrap img-wrap--grid">
                        <svg class="lp lp--grid">
                            <use xlink:href="#icon-lp-mini"></use>
                        </svg>
                        <img class="img img--grid" src="${recommendation['album_cover_image_url']}" alt="${recommendation['album_name']}" />
                    </div>
                    <span class="year">${recommendation['album_release_date']}</span>
                    <h2 class="artist">
                        <span>${recommendation["artists"].join(', ')}</span>
                    </h2>
                    <h3 class="title">${recommendation['track_name']}</h3>
                </a>
            </li>
            `
        recommendationsContent += recItem
    }
    // add recommendations to page
    recommendationsContainer.innerHTML = recommendationsContent

    // NOTE: Attach the like button click event listener for new nodes added to the DOM.
    // This step is important to ensure that the button clicks work
    LikeEventListener();
}

/**
 * Attach click event listener to floating action button
 */
document.querySelector(".fab").addEventListener('click', () => {
    document.querySelector(".popover-container").classList.toggle('popover-active');
    let fabIcon = document.querySelector(".fab-icon")
    fabIcon.textContent = fabIcon.textContent == "forum" ? "close" : "forum"
});

/**
 * Attach click event listener to recommendations button
 */
document.querySelector("#recommendation-btn").addEventListener("click", async (e) => {
    e.preventDefault()

    let chatbotForm = document.forms.namedItem("chatbot-form");
    const formData = new FormData(chatbotForm)

    // get the form data, transform it to lowercase and then parse it to a json string
    let formDataJson = JSON.stringify(Object.fromEntries(formData.entries())).toLocaleLowerCase();

    // check if the user is already logged in
    let isLoggedIn = document.cookie.trim().length > 1 && document.cookie.includes("remember_token");
    if (isLoggedIn) {
        // request the new data
        try {
            let response = await fetch("/api/recommendations", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: formDataJson
            })

            // update the page with the new recommendations
            response.json().then(recommendations => {
                UpdatePage(recommendations);
                // show a message on success
                let toast = new Snacky({ actionButton: true, actionText: "Dismiss" });
                toast.show("New recommendations loaded");
            });
        } catch (error) {
            // @TODO: Handle errors properly
            throw new Error(error);
        }
    }
    else {
        let toast = new Snacky({ duration: 8000 });
        toast.show("Please login to use this feature");
    }
});