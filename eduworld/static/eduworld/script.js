document.addEventListener('DOMContentLoaded', function ()
{
  document.querySelector('#student').addEventListener('click', () => cadastro('student'));
  document.querySelector('#teacher').addEventListener('click', () => cadastro('teacher'));
});


function cadastro(tipo)
{
  var x = document.getElementById("inicio");
  x.style.display = "none";


  if (tipo === "teacher")
  {
  document.querySelector('#formulario').innerHTML =
    `

        <label class="my-1 mr-2" for="inlineFormCustomSelectPref">Title</label>
        <select class="custom-select my-1 mr-sm-2" id="inlineFormCustomSelectPref" required name="titulo">
          <option selected style="color:gray;">Chose...</option>
          <option value="Miss">Miss</option>
          <option value="Mrs.">Mrs.</option>
          <option value="Dr.">Dr.</option>
          <option value="Professor">Professor</option>
        </select>


        <label class="my-1 mr-2" for="inlineFormCustomSelectPref">Name</label>
        <div class="input-group">
        <input required name="firstname" type="text" class="form-control" placeholder="First Name"/>
        <div class="input-group-prepend">
            <span class="input-group-text" id=""></span>
        </div>
        <input required name="lastname" type="text" class="form-control" placeholder="Last Name"/>
      </div>

      <br><br>
      <div class="form-group">
                  <input class="btn btn-primary btn-lg button1" type="submit" value="Register">
      </div>


    `;
  }
  else
  {
    if (tipo === "student")
    {
    document.querySelector('#formulario').innerHTML =
      `
          <label class="my-1 mr-2" for="inlineFormCustomSelectPref">Name</label>
          <div class="input-group">
          <input required name="firstname" type="text" class="form-control" placeholder="First Name"/>
          <div class="input-group-prepend">
              <span class="input-group-text" id=""></span>
          </div>
          <input required name="lastname" type="text" class="form-control" placeholder="Last Name"/>
        </div>

          <label class="my-1 mr-2" for="inlineFormCustomSelectPref">Education</label>
          <select class="custom-select my-1 mr-sm-2" id="inlineFormCustomSelectPref" required name="education">
            <option selected style="color:gray;">Chose...</option>
            <option value="Primary [elementary] School">Primary [elementary] School</option>
            <option value="Midle School">Midle School</option>
            <option value="Secondary [high] School">Secondary [high] School</option>
            <option value="Postsecondary [tertiary] Education">Postsecondary [tertiary] Education</option>
          </select>


        <div class="form-group">
        <label class="my-1 mr-2" for="inlineFormCustomSelectPref">School</label>
        <input type="text" class="form-control" id="school" name="escola">
      </div>

        <br><br>
        <div class="form-group">
                    <input class="btn btn-primary btn-lg button1" type="submit" value="Register">
        </div>


      `;
    }
  }
}