document.getElementById("btn-client").addEventListener('click', function(e) {
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
                    const option=document.createElement("option")
                    option.textContent=data[i].pseudo
                    userconnecteds.appendChild(option)
                    i++
                })
            }
        })
    }
})
filluserconnecteds()