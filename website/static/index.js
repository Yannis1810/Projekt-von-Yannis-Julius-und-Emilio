function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/notes1";
  });
}

function deleteRepair(repairId) {
  fetch("/delete-repair", {
    method: "POST",
    body: JSON.stringify({ repairId: repairId }),
  }).then((_res) => {
    window.location.href = "/repairs";
  });
}