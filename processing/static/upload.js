      // {#        var video = document.querySelector("#video");#}
      // {#        var recordButton = document.querySelector("#recordButton");#}
      // {#        var fileInput = document.querySelector('#videoInput');#}
      // {##}
      // {#        var mediaRecorder;#}
      // {#        var chunks = [];#}
      // {#        var isRecording = false; // State to track if recording is active#}
      // {##}
      // {#        if (navigator.mediaDevices.getUserMedia) {#}
      // {#            navigator.mediaDevices.getUserMedia({ video: true })#}
      // {#            .then(function (stream) {#}
      // {#                video.srcObject = stream;#}
      // {##}
      // {#                mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs="vp8, opus"' });#}
      // {##}
      // {#                mediaRecorder.ondataavailable = function (e) {#}
      // {#                    if (e.data.size > 0) {#}
      // {#                        chunks.push(e.data);#}
      // {#                    }#}
      // {#                };#}
      // {##}
      // {#                mediaRecorder.onstop = function () {#}
      // {#                    var blob = new Blob(chunks, { type: 'video/webm' });#}
      // {#                    chunks = [];#}
      // {##}
      // {#                var file = new File([blob], "./recorded-video.mp4", {#}
      // {#                  type: "video/mp4",#}
      // {#                });#}
      // {##}
      // {#                var dataTransfer = new DataTransfer();#}
      // {#                dataTransfer.items.add(file);#}
      // {##}
      // {#                // Set the DataTransfer object to the file input#}
      // {#                fileInput.files = dataTransfer.files;#}
      // {#                console.log("hope this worked");#}
      // {#                // fileInput.files = [file];#}
      // {#                uploadForm.submit();#}
      // {##}
      // {#                // var downloadLink = document.createElement('a');#}
      // {#                // downloadLink.href = URL.createObjectURL(blob);#}
      // {#                // downloadLink.download = 'recorded-video.mp4';#}
      // {#                // document.body.appendChild(downloadLink);#}
      // {#                // downloadLink.click();#}
      // {#                // document.body.removeChild(downloadLink);#}
      // {#              };#}
      // {#            })#}
      // {#            .catch(function (error) {#}
      // {#              console.log("Something went wrong!");#}
      // {#            });#}
      // {#        }#}
      // {##}
      // {#        // Handle record button click#}
      // {#        recordButton.addEventListener("click", function () {#}
      // {#          if (mediaRecorder.state === "inactive") {#}
      // {#            // Start recording#}
      // {#            mediaRecorder.start();#}
      // {#            recordButton.textContent = "Stop Recording";#}
      // {#          } else {#}
      // {#            // Stop recording#}
      // {#            mediaRecorder.stop();#}
      // {#            recordButton.textContent = "Record";#}
      // {#          }#}
      // {#        });#}
      // {##}
              // file drag-and-drop functionality
              var dropzone = document.getElementById("dropzone");
              var fileInfo = document.getElementById("file-info");
              var fileNameElement = document.getElementById("file-name");

              function handleFile(file) {
                fileNameElement.textContent = file.name;
                fileInfo.classList.remove("hidden");
              }

              dropzone.addEventListener("dragover", (e) => {
                e.preventDefault();
                dropzone.classList.add("border-indigo-600");
              });

              dropzone.addEventListener("dragleave", (e) => {
                e.preventDefault();
                dropzone.classList.remove("border-indigo-600");
              });

              dropzone.addEventListener("drop", (e) => {
                e.preventDefault();
                dropzone.classList.remove("border-indigo-600");
                var file = e.dataTransfer.files[0];
                handleFile(file);
              });

              var input = document.getElementById("videoInput");

              input.addEventListener("change", (e) => {
                var file = e.target.files[0];
                handleFile(file);
              });

              document.querySelectorAll(".theme-card").forEach((card) => {
                card.addEventListener("click", function () {
                  const theme = this.getAttribute("data-theme");
                  document.getElementById("theme").value = theme;
                  // Optionally, add some visual feedback for selection
                });
              });


              // toggle background
              function toggleBackground(cardNumber) {
                  console.log(cardNumber);
            // Iterate through all the cards and reset their backgrounds
            for (let i = 1; i <= 6; i++) {
              const card = document.getElementById(`character-card-${i}`);
              card.classList.remove('bg-sky-300');
              card.classList.add('bg-slate-600');
            }

            // Toggle the background of the clicked card
            const clickedCard = document.getElementById(`character-card-${cardNumber}`);
            clickedCard.classList.remove('bg-slate-600');
            clickedCard.classList.add('bg-sky-300');
          }


          // Globals
  let mediaRecorder;
  let recordButton = document.getElementById('recordButton');
  let stopButton = document.getElementById('stopButton');
  let videoElement = document.getElementById('input_video');

  function initMediaStream() {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        videoElement.srcObject = stream;
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
          if (event.data.size > 0) {
            // Handle recorded data
          }
        };

        mediaRecorder.onstop = () => {
          // Handle stop recording
          videoElement.srcObject.getTracks().forEach(track => track.stop()); // Stop the video stream
        };
      })
      .catch(error => {
        console.error("Error accessing media devices:", error);
      });
  }

  recordButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'inactive') {
      mediaRecorder.start();
      recordButton.textContent = 'Stop Recording';
    }
  });

  stopButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
      mediaRecorder.stop();
      recordButton.textContent = 'Record';
    }
  });

  window.addEventListener('load', initMediaStream);

              function onResults(results) {
                  canvasCtx.save();
                  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                  canvasCtx.drawImage(results.image, 0, 0, canvasElement.width
      , canvasElement.height);
                  if (results.multiFaceLandmarks) {
                  for (const landmarks of results.multiFaceLandmarks) {
                      // Improved drawing style for a fancier look
                      drawConnectors(canvasCtx, landmarks, FACEMESH_TESSELATION, { color: '#ffffff', lineWidth: 0.5 });
                      drawConnectors(canvasCtx, landmarks, FACEMESH_RIGHT_EYE, { color: '#32cd32', lineWidth: 1 });
                      drawConnectors(canvasCtx, landmarks, FACEMESH_LEFT_EYE, { color: '#32cd32', lineWidth: 1 });
                      drawConnectors(canvasCtx, landmarks, FACEMESH_LIPS, { color: '#24a0ed', lineWidth: 1 });
                  }
              }

              // Emotion Detection Display
              // {#canvasCtx.font = '10px Arial';#}
              // {#canvasCtx.fillStyle = 'yellow';#}
              // {#canvasCtx.fillText(`Emotion: ${emotions}`, canvasElement.width - 80, 15);#}

              canvasCtx.restore();
          }

          const faceMesh = new FaceMesh({
              locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
          });
          faceMesh.setOptions({
              maxNumFaces: 5,
              refineLandmarks: true,
              minDetectionConfidence: 0.5,
              minTrackingConfidence: 0.5
          });
          faceMesh.onResults(onResults);

          new Camera(videoElement, {
              onFrame: async () => {
                  await faceMesh.send({ image: videoElement });
              },
              width: 640,
              height: 480
          }).start();