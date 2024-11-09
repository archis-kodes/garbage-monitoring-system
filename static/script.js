const flaskEndpoint = "http://192.168.137.139:5000/get_bin_levels";



function updateBinLevel(bioLevel, eLevel, nonBioLevel) {

    const bioProgressBar = document.getElementById("bio-progress-bar");

    const bioProgressText = document.getElementById("bio-progress-text");

    const eProgressBar = document.getElementById("ewaste-progress-bar");

    const eProgressText = document.getElementById("ewaste-progress-text");

    const nonBioProgressBar = document.getElementById("nonbio-progress-bar");

    const nonBioProgressText = document.getElementById("nonbio-progress-text");



    bioProgressBar.style.height = `${bioLevel}%`;

    bioProgressText.innerText = `${bioLevel}%`;



    eProgressBar.style.height = `${eLevel}%`;

    eProgressText.innerText = `${eLevel}%`;



    nonBioProgressBar.style.height = `${nonBioLevel}%`;

    nonBioProgressText.innerText = `${nonBioLevel}%`;





    if (bioLevel > 70) {

        showModal(`Clean Wet Bin: ${bioLevel}%`);

    } else if (nonBioLevel > 70) {

        showModal(`Clean Dry Bin: ${nonBioLevel}%`);

    } else if (eLevel > 70) {

        showModal(`Clean Metal Bin: ${eLevel}%`);

    }

}



function showModal(message) {

    const modal = document.getElementById("warning-modal");

    const modalMessage = document.getElementById("modal-message");

    modalMessage.innerText = message;

    modal.style.display = "flex";

}



function closeModal() {

    const modal = document.getElementById("warning-modal");

    modal.style.display = "none";

}



function fetchDataAndUpdate() {

    fetch(flaskEndpoint)

        .then(response => response.json())

        .then(data => {

            updateBinLevel(data[0], data[1], data[2]);

        })

        .catch(error => console.error("Error fetching data:", error));

}



setInterval(fetchDataAndUpdate, 5);

