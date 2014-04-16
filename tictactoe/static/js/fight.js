(function ($, global) {
    var tpl = $(
        '<table>\
          <tr><td></td><td></td><td></td></tr>\
          <tr><td></td><td></td><td></td></tr>\
          <tr><td></td><td></td><td></td></tr>\
        </table>').addClass("board");

    var Board = function(i_gameplay, rootnode) {
        this.gameplay = i_gameplay;
        this.board = board_init(rootnode);
        this.state_reset();
        rootnode.append(this.board);
    };

    Board.prototype.put = function(what, n) {
        var stupidlist = num_to_coords(n);
        var x1 = stupidlist[0];
        var y1 = stupidlist[1];
        var x2 = stupidlist[2];
        var y2 = stupidlist[3];
        this.board.find("tr.outer").eq(x1).
            find("td.outer").eq(y1).
            find("tr.inner").eq(x2).
            find("td.inner").eq(y2).text(what)
    }

    Board.prototype.flip = function() {
        return this.xo = this.xo == 'x' ? 'o' : 'x';
    }

    Board.prototype.board_reset = function() {
        this.state_reset();
        this.board.find("td.inner").text("");
    }

    Board.prototype.state_reset = function() {
        this.current_pos = -1;
        this.xo = 'o';
    }

    Board.prototype.forward = function() {
        if (this.current_pos >= this.gameplay.length - 1)
            return;
        this.put(this.flip(), this.gameplay[++this.current_pos]);
    }

    Board.prototype.backward = function() {
        if (this.current_pos < 0)
            return;
        this.flip();
        this.put("", this.gameplay[this.current_pos--]);
    }

    Board.prototype.fastforward = function() {
        if (this.current_pos >= this.gameplay.length)
            this.board_reset();
        while (this.current_pos < this.gameplay.length - 1)
            this.forward();
    }

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

    function board_init() {
        var inner = tpl.clone(); var outer = tpl.clone();
        inner.find("tr,td").addBack().addClass("inner");
        outer.find("tr,td").addBack().addClass("outer");
        outer.find("td.outer").each(function() {
            $(this).html(inner.clone());
        });
        return outer;
    }

    global.Board = Board
})(jQuery, this)
