(function ($, global) {
    "use strict";

    var tpl = $(
        '<table>\
          <tr><td></td><td></td><td></td></tr>\
          <tr><td></td><td></td><td></td></tr>\
          <tr><td></td><td></td><td></td></tr>\
        </table>'
    ).addClass("board");

    var Board = function (i_gameplay, boardnode, statusnode) {
        this.reset_callbacks = [];
        this.forward_callbacks = [];
        this.backward_callbacks = [];
        this.statusnode = statusnode;
        this.gameplay = i_gameplay;
        this.board = board_init(boardnode);
        this.state_reset();
        boardnode.append(this.board);
    };

    Board.prototype.put = function (what, n) {
        var stupidlist = num_to_coords(n),
            x1 = stupidlist[0] - 1,
            y1 = stupidlist[1] - 1,
            x2 = stupidlist[2] - 1,
            y2 = stupidlist[3] - 1;
        this.board.find("tr.outer").eq(x1).
            find("td.outer").eq(y1).
            find("tr.inner").eq(x2).
            find("td.inner").eq(y2).text(what);
    };

    Board.prototype.flip = function () {
        this.xo = this.xo === 'x' ? 'o' : 'x';
        return this.xo;
    };

    Board.prototype.board_reset = function () {
        this.state_reset();
        this.statusnode.children().remove();
        this.board.find("td.inner").text("");
    };

    Board.prototype.state_reset = function () {
        this.current_pos = -1;
        this.xo = 'o';
    };

    Board.prototype.forward = function () {
        if (this.current_pos >= this.gameplay.length - 1)
            return;
        var xo = this.flip(),
            pos = this.gameplay[++this.current_pos];

        var t = this.xo + " placed on (" + pos.toString() + ")";
        this.statusnode.append($("<div/>").html(t));

        this.put(xo, pos);
    };

    Board.prototype.backward = function () {
        if (this.current_pos < 0)
            return;
        this.flip();
        this.statusnode.children().last("<div>").remove();
        this.put("", this.gameplay[this.current_pos--]);
    };

    Board.prototype.fastforward = function () {
        if (this.current_pos >= this.gameplay.length)
            this.board_reset();
        while (this.current_pos < this.gameplay.length - 1)
            this.forward();
    };

    function num_to_coords(n) {
        // 1..81 => x1, y1, x2, y2 minus one.
        var rowm = Math.floor((n - 1) / 9),
            colm = (n - 1) % 9,
            x1 = Math.floor(rowm / 3),
            y1 = Math.floor(colm / 3),
            x2 = rowm % 3,
            y2 = colm % 3;
        return [x1+1, y1+1, x2+1, y2+1];
    }

    function board_init() {
        var inner = tpl.clone(), outer = tpl.clone();
        inner.find("tr,td").addBack().addClass("inner");
        outer.find("tr,td").addBack().addClass("outer");
        outer.find("td.outer").each(function () {
            $(this).html(inner.clone());
        });
        return outer;
    }

    global.Board = Board
})(jQuery, this)
