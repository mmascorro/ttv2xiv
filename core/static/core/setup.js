const resultsContainer = document.getElementById('search_results');
const xivNameDisplay = document.getElementById('xiv_name');
const xivWorldSelect = document.getElementById('xiv_world_select');
const xivNameInput = document.getElementById('xiv_name_input');
const xivProgressBar = document.getElementById('xiv-progress');
const entryTemplate = document.getElementById('entry-template');
const deleteButton = document.getElementById('delete-button');

function createMessage(message, cssClass) {
  const div = document.createElement('div');
  div.classList.add('message');
  div.classList.add(cssClass);
  const p = document.createElement('p');
  p.classList.add('message-body');
  p.innerHTML = message;
  div.appendChild(p);
  return div;
}

document.getElementById('xiv_form').addEventListener('submit', async (e) => {

  e.preventDefault();
  clearResults();
  xivProgressBar.classList.remove('is-hidden')

  const nameQuery = encodeURI(xivNameInput.value)
  const worldQuery = xivWorldSelect.value;

  let response = await fetch(`/lodestone_search/${worldQuery}/${nameQuery}/`, {
    credentials: "include",
  });

  if (response.status === 200) {
    let data = await response.text();
    const parser = new DOMParser();
    const doc = parser.parseFromString(data, 'text/html');
    const entryLinks = doc.querySelectorAll('.entry__link');
    if (entryLinks.length > 0) {
      let searchResults = [];
      
      entryLinks.forEach(el => {
        const entry = {
          name: el.querySelector('.entry__name').innerText,
          id: el.href.match(/character\/(\d+)/)[1],
          img: el.querySelector('.entry__chara__face img').src
        };
        searchResults.push(entry);
      });
  
      resultsContainer.innerHTML = '';
  
      searchResults.forEach(sr => {
  
        const entry = entryTemplate.content.cloneNode(true);
        const div = entry.querySelector('.media');
        div.dataset.xivId=sr.id;
        entry.querySelector('img').src = sr.img;
        entry.querySelector('p').innerHTML = sr.name;
        
        div.addEventListener('click', e => {
          lodestone_check(sr.id)
        })
        resultsContainer.appendChild(entry);
      });
  
      xivProgressBar.classList.add('is-hidden')
      document.getElementById('result-instruction').classList.remove('is-hidden')
  
    } else {
      xivProgressBar.classList.add('is-hidden')

      const divMessage = createMessage("No results from FFXIV Lodestone", 'is-warning');
      resultsContainer.appendChild(divMessage);
    }
  } else {
    xivProgressBar.classList.add('is-hidden')

    const divMessage = createMessage("Error getting data from FFXIV Lodestone", 'is-danger');
    resultsContainer.appendChild(divMessage);

  }
  
});

async function lodestone_check(id) {

  xivProgressBar.classList.remove('is-hidden');
  let response = await fetch(`/lodestone_check/${id}/`, {
    credentials: "include",
  });
  if (response.status === 200) {
    let data = await response.json();
    if ('xiv_name' in data) {
      xivNameDisplay.innerHTML = data.xiv_name;
      clearResults();
      xivNameInput.value = '';
      xivWorldSelect.value = '';
      xivProgressBar.classList.add('is-hidden');
      document.getElementById('result-instruction').classList.add('is-hidden');
    } else { 
      //error
    }

  } else {
    xivProgressBar.classList.add('is-hidden');
    alert('error')
  }

}

function clearResults() {
  //clear any results and event handlers
  resultsContainer.innerHTML = '';
}

deleteButton.addEventListener('click', e => {
  e.preventDefault();
  
  if (confirm('Confirm information deletion')) {
    location.assign('/delete/');
  }
  
})