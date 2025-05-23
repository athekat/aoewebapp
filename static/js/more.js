function toggleDescription(button) {
    const descriptionDiv = button.closest('.mb-3').querySelector('.civ-description');
    if (descriptionDiv) {
        const isHidden = descriptionDiv.classList.contains('d-none');
        descriptionDiv.classList.toggle('d-none');
        button.textContent = isHidden ? "Hide Details" : "Civ Info";
    }
}
