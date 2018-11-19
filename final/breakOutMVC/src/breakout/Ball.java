/**
 *Eric Stadelman and Charlie Broadbent
 *  Ball.java
 * A subclass used to represent, set values and move our ball
 */
package breakout;

import javafx.fxml.FXML;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;

public class Ball extends Circle {
    @FXML private double velocityX;
    @FXML private double velocityY;


    public Ball() {
        this.setStroke(Color.BLACK);
    }

    public void reset(){
        this.setCenterY(200);
        this.setCenterX(75);
        this.setVelocityX(-5);
        this.setVelocityY(5);
    }

    public void step() {
        this.setCenterX(this.getCenterX() + this.velocityX);
        this.setCenterY(this.getCenterY() + this.velocityY);
    }

    public double getVelocityX() {
        return velocityX;
    }

    public void setVelocityX(double velocityX) {
        this.velocityX = velocityX;
    }

    public double getVelocityY() {
        return velocityY;
    }

    public void setVelocityY(double velocityY) {
        this.velocityY = velocityY;
    }
}


