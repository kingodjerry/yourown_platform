document.addEventListener('DOMContentLoaded', () => {
    let container = document.getElementById('container');
    if (container) {
        setTimeout(() => {
            container.classList.add('sign-in');
        }, 200);
    } else {
        console.error("Container element not found.");
    }
});

function toggle() {
	container.classList.toggle('sign-in');
	container.classList.toggle('sign-up');
}