console.log("Hello world")
const postsbox = document.getElementById("posts-box")
const spinnerbox = document.getElementById("spinner-box")
const loadbtn = document.getElementById("loadbtn")
const loadbox = document.getElementById("loading-box")

let visible = 5

const getdata = () =>{
    $.ajax({
        type: 'GET',
        url: `posts-json/${visible}`,
        success: function(response){
            const data = response.data
            const nomes = response.nome
            const fotos = response.foto
            const maxSize = response.max
            const classe = response.CLASSE
            let i = 0
            console.log(nomes[0])
            document.getElementById("spinner-box").classList.remove("apagado")
            setTimeout(()=>{
                document.getElementById("spinner-box").classList.add("apagado")
                data.map(post=>{
                    console.log(post.id)
                    console.log(i)
                    document.getElementById("posts-box").innerHTML += `<div class="ml-4">
                    <div class="d-flex align-items-start profile-feed-item">
                      <img src="/media/${fotos[i]}" alt="${nomes[i]} profile photo" class="img-sm rounded-circle">
                      <div class="ml-4">
                        <h6>
                          <a href="/profile/${post.dono_id}" class="class_link" target="_blank">${nomes[i]}</a>
                          <small class="ml-4 text-muted"><i class="mdi mdi-clock mr-1"></i>${formatDate(post.data)}</small>
                        </h6>
                        <p>
                          ${post.post_text}
                        </p>
                        <p class="small text-muted mt-2 mb-0">
                          <span class="ml-2">
                          <a href="/classroom/${classe}/post/${post.id}" class="class_link">See more</a>
                          </span>
                        </p>
                      </div>
                  </div>
                </div>`
                i += 1
                })
                if(maxSize){
                    console.log("done")
                    document.getElementById("loading-box").innerHTML = "<h4><h4>"
                }
            }, 500)

        },
        error: function(error){
            console.log(error)
        }
    })
}

getdata()


document.addEventListener('DOMContentLoaded', function ()
{
  document.querySelector('#loadbtn').addEventListener('click', () => {visible += 5, getdata()});
});


function formatDate(date)
{
    const chars = date.split("T");
    let data = chars[0] // OK
    let hora = chars[1]
    hora = hora.split(".")
    hora = hora[0]
    console.log(data)
    console.log(hora)

    let horas =  hora.split(":")
    console.log(horas[0]) // VALOR DA HORA
    console.log(horas[1]) //VALOR DO MINUTO


    let update = `${data}, ${horas[0]}:${horas[1]}`
    return update
}
