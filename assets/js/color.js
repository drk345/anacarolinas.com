var blues = [
  { name: 'Salvia (elección Ana)', hex: '#B7C9CD', tag: 'original', desc: 'El tono que Ana eligió. Desaturado y cálido, convive sin tensión con la terracota.' },
  { name: 'Eau de nil', hex: '#9DBFC0', tag: 'cálido', desc: 'Más verde que azul. Evoca estética vintage francesa — funciona muy bien con Spectral.' },
  { name: 'Polvo claro', hex: '#CCDDE1', tag: 'suave', desc: 'Casi neutro. Sustituye al cream en secciones alternadas sin romper la calidez.' },
  { name: 'Haze marino', hex: '#95A8AD', tag: 'versátil', desc: 'Mid-tone equilibrado. Funciona tanto de fondo como de color de texto secundario.' },
  { name: 'Gris pizarra', hex: '#8499AF', tag: 'neutro', desc: 'Más hacia el azul. El contraste frío-cálido con la terracota es marcado y elegante.' },
  { name: 'Teal profundo', hex: '#2C5058', tag: 'intenso', desc: 'Oscuro y contrastado. Sustituiría al olive como color estructural, no como fondo.' }
];

var grid = document.getElementById('blueGrid');
var comboBlue = document.getElementById('comboBlue');
var stripBlue = document.getElementById('stripBlue');
var stripLbl = document.getElementById('stripBlueLbl');
var fullBlue = document.getElementById('fullBlue');
var fullBlueLbl = document.getElementById('fullBlueLbl');

blues.forEach(function(b, i) {
  var card = document.createElement('div');
  card.className = 'blue-card' + (i === 0 ? ' sel' : '');
  card.innerHTML =
    '<div class="blue-swatch-block blue-swatch--' + i + '"></div>' +
    '<div class="blue-info">' +
      '<div class="blue-name">' + b.name + '</div>' +
      '<div class="blue-hex-lbl">' + b.hex + '</div>' +
      '<div class="blue-desc">' + b.desc + '</div>' +
      '<span class="blue-tag">' + b.tag + '</span>' +
    '</div>';
  card.addEventListener('click', function() {
    document.querySelectorAll('.blue-card').forEach(function(c) { c.classList.remove('sel'); });
    card.classList.add('sel');
    apply(i, b.hex);
  });
  grid.appendChild(card);
});

function apply(i, hex) {
  comboBlue.className = 'combo-sec combo-blue--' + i;
  stripBlue.className = 'sw--b' + i;
  fullBlue.className = 'sw--b' + i;
  stripLbl.textContent = hex;
  fullBlueLbl.textContent = hex;
}
