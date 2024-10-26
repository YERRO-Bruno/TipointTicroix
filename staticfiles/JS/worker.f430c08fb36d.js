alert("worker")
console.log("in worker")
onmessage = (e) => {
  postMessage("message bien reçu de worker : "+e.data[0])
}