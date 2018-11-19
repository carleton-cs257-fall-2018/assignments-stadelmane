/**
 * Eric Stadelman and Charlie Broadbent
 * Brick.java
 * A subclass used to represent, set values and keep track of values
 * including boolean to remove or not.
 */



package breakout;

import javafx.scene.shape.Rectangle;
import javafx.scene.paint.Color;

public class Brick extends Rectangle {
    private int hitsLeft;

    public Brick(double x, double y){
        this.setWidth(100);
        this.setHeight(25);
        //we decided to only allow one hit per brick, but could easily change this variable
        this.hitsLeft = 0;
        this.setX(x*145 + 10);
        this.setY(y * 50 + 25);
        this.setFill((Color.color(Math.random(), Math.random(), Math.random())));
        this.setStroke(Color.BLACK);
    }

    public boolean isDestroyed(){
        if (this.hitsLeft<0) {
            return true;
        }
        else{
            return false;
        }
    }

    public void hit(){
        this.hitsLeft--;
        }
}

