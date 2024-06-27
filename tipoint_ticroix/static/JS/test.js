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
                    const option=document.createElement("option")
                    option.textContent=data[i].pseudo
                    userconnecteds.appendChild(option)
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