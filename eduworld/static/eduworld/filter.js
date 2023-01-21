console.log('Hi')

$(document).ready(function(){
	$(".filter-checkbox, #FilterBtn").on('click',function(){

        console.log('escolhi categoria')
        var category = $('#categoryform').find(":selected").val();
        console.log(category)
        document.getElementById('filtereddata').innerHTML = " "

        $.ajax({
            type: 'POST',
            url: '/filter-form-data',
            data: {
                category: category,
                action: 'post'
            },
			success:function(res){
				console.log(res.status);
                console.log(res.dt);

                data = res.dt
                tamanho = data.length

                let paginator = document.getElementById(`paginator`)
                let alldata = document.getElementById(`alldata`)
                paginator.classList.add("apagado");
                alldata.classList.add("apagado");

                if (tamanho === 0)
                {
                    document.getElementById('filtereddata').innerHTML = `There are no questions in this category yet!`;
                }
                else
                {
                    let i = 0
                    data.map(post=>{
                        console.log(post.id)
                        console.log(i)
                        document.getElementById('filtereddata').innerHTML += `<!-- End of post ${i} -->
                        <div class="card row-hover pos-relative py-3 px-3 mb-3 border-info border-top-0 border-right-0 border-bottom-0 rounded-0">
                          <div class="row align-items-center">
                            <div class="col-md-8 mb-3 mb-sm-0">
                              <h5>
                                <a href="/forum/question/${post.id}" class="text-primary">${post.titulo}</a>
                              </h5>
                              <p class="text-sm"><span class="op-6">Posted</span> <span class="text-black">${formatDate(post.data)}</span><span class="op-6">, by</span> <a class="text-black" href="/profile/${post.dono_id}" style="color:gray;">${post.dono_id__username}</a></p>
                              <div class="text-sm op-5"> <a class="text-black mr-2" href="#">#${post.category}</a> </div>
                            </div>
                            <div class="col-md-4 op-7">
                              <div class="row text-center op-7">
                                <div class="col px-1"> <i class="ion-ios-chatboxes-outline icon-1x"></i> <span class="d-block text-sm">${post.reply_count} Replies</span> </div>
                                <div class="col px-1"> <i class="ion-ios-eye-outline icon-1x"></i> <span class="d-block text-sm">${post.views} Views</span> </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <!-- /End of post ${i} -->`
                    i += 1
                    })
                }

			}
		});
	});

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