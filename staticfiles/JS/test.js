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
                    const li=document.createElement("a")
                    li.textContent=data[i].pseudo
                    li.id=data[i].pseudo
                    li.class="joueur"
                    li.href='action'
                    if (data[i].pseudo==pseudox) {
                        //alert(pseudox)
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
})
document.getElementsByClassName("joueur").addEventListener("click", function(e) {
    e.preventDefault()
    alert("click joueur")
    alert(e.target.id)
})

