document.addEventListener("DOMContentLoaded", function () {
    alert("client")
  
    function filluserconnecteds() {
        const userconnecteds=document.getElementById("id_userconnecteds")
        $.ajax({
            url:'/api/userconnecteds',
            method: "GET",
            dataType: "json",
            success: function (data) {
                var i = 0;
                data.forEach(userconnected => {
                    alert("success")
                    const li=document.createElement("li")
                    li.textContent=data[i].pseudo
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
})