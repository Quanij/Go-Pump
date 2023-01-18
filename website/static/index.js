function deletePressure(pressureId) {
  fetch("/delete-pressure", {
    method: "POST",
    body: JSON.stringify({ pressureId: pressureId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
