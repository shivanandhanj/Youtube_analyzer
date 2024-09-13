document.getElementById('analyze-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const videoUrl = document.getElementById('video_url').value;
    const question = document.getElementById('question').value;

    const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_url: videoUrl, question: question })
    });

    const data = await response.json();

    document.getElementById('transcript').innerText = JSON.stringify(data.transcript, null, 2);
    document.getElementById('summary').innerText = data.summary;
    document.getElementById('answer').innerText = data.answer;
});

document.getElementById('analyze-details').addEventListener('submit', function (e) {
    e.preventDefault();
    const videoUrl = document.getElementById('video_url').value;

    fetch('/details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_url: videoUrl })
    })
    .then(response => response.json())
    .then(data => {
        // Show result div
        document.getElementById('result').style.display = 'block';
        
        // Populate the video details
        document.getElementById('title').innerText = data.title;
        document.getElementById('description').innerText = data.description;
        document.getElementById('views').innerText = data.views;
        document.getElementById('likes').innerText = data.likes;
        document.getElementById('comments').innerText = data.comments;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('analyze-comment').addEventListener('submit', function (e) {
    e.preventDefault();
    
    const videoUrl = document.getElementById('video_url').value;

    fetch('/comment-details', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_url: videoUrl })
    })
    .then(response => response.json())
    .then(data => {
        // Clear previous comments before injecting new ones
        document.getElementById('top-comments-section').innerHTML = '';
        document.getElementById('timestamp-comments-section').innerHTML = '';
        document.getElementById('all-comments-section').innerHTML = '';

        // Populate the top comments (most liked) if it's an array
        if (Array.isArray(data.top_comments)) {
            data.top_comments.forEach(comment => {
                const commentElement = document.createElement('p');
                commentElement.innerHTML = `<strong>${comment.author}:</strong> ${comment.text} <span>(Likes: ${comment.likes})</span>`;
                document.getElementById('top-comments-section').appendChild(commentElement);
            });
        }

        // Populate the timestamped comments if it's an array
        if (Array.isArray(data.timestamped_comments)) {
            data.timestamped_comments.forEach(comment => {
                const commentElement = document.createElement('p');
                commentElement.innerHTML = `<strong>${comment.author}:</strong> ${comment.text} <a href="#${comment.timestamp}" onclick="goToTimestamp('${comment.timestamp}')">[${comment.timestamp}]</a>`;
                document.getElementById('timestamp-comments-section').appendChild(commentElement);
            });
        }

        // Populate all comments if it's an array
        if (Array.isArray(data.all_comments)) {
            data.all_comments.forEach(comment => {
                const commentElement = document.createElement('p');
                commentElement.innerHTML = `<strong>${comment.author}:</strong> ${comment.text} <span>(Likes: ${comment.likes})</span>`;
                document.getElementById('all-comments-section').appendChild(commentElement);
            });
        }
    })
    .catch(error => {
        console.error('Error fetching comment details:', error);
    });
});
