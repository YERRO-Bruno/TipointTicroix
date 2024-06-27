document.addEventListener("DOMContentLoaded", function () {
    function filluserconnecteds() {
        const userconnecteds=document.getElementById("id_userconnecteds")
        const pseudox=document.getElementById("id-connec").textContent
        $.ajax({
            url:'/api/userconnecteds',
            method: "GET",
            dataType: "json",
            success: function (data) {
                var i = 0;
                data.forEach(userconnected => {
                    alert("success")
                    const li=document.createElement("a")
                    li.textContent=data[i].pseudo
                    if (data[i].pseudo==pseudox) {
                        alert(pseudox)
                        li.style.color='blue'
                        li.style.fontWeight='1000'
                    }
                    userconnecteds.appendChild(li)
                    i++
                })
            },
            error: function (xhr, status, error) {
                alert("error")

            }
        })
    }
    filluserconnecteds()
    document.getElementById("id-userconnecteds").addEventListener("click", function(event) {
        alert(event.target.textContent)
    })
})