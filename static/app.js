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
