function num_to_coords(n) {
  // 1..81 => x1, y1, x2, y2 minus one.
  var rowm = Math.floor((n - 1) / 9);
  var colm = (n - 1) % 9;
  var x1 = Math.floor(rowm / 3);
  var y1 = Math.floor(colm / 3);
  var x2 = rowm % 3;
  var y2 = colm % 3;
  return [x1, y1, x2, y2];
}

function put(what, n) {
  [x1, y1, x2, y2] = num_to_coords(n);
  $("tr.outer").eq(x1).
    find("td.outer").eq(y1).
    find("tr.inner").eq(x2).
    find("td.inner").eq(y2).text(what)
}


function flip() {
  xo = xo == 'x' ? 'o' : 'x';
  return xo;
}

function forward() {
  if (current_pos >= gameplay.length - 1)
    return;
  put(flip(), gameplay[++current_pos]);
}

function backward() {
  flip()
  put("", gameplay[current_pos--]);
}

function fastforward() {
  if (current_pos >= gameplay.length)
    board_reset();
  while (current_pos < gameplay.length - 1)
    forward();
}

function board_reset() {
  state_reset();
  $("table.board td.inner").text("");
}

function state_reset() {
  current_pos = -1;
  xo = 'o';
}

function board_init() {
  var tpl = $("table.board").clone().addClass("inner");
  $("table.board, table.board td, table.board tr").addClass("outer");
  tpl.find("tr,td").addClass("inner");
  $("table.outer > tbody > tr > td").html(tpl);
}

$(function() {
  state_reset();
  board_init();
  $("#reset").click(board_reset);
  $("#forward").click(forward);
  $("#backward").click(backward);
  $("#fastforward").click(fastforward);
});
