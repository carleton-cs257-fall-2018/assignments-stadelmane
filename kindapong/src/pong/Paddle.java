package pong;

import javafx.fxml.FXML;
import javafx.scene.shape.Rectangle;

public class Paddle extends Rectangle {
    private double velocityX;

    @FXML private double setLayoutX;
    @FXML private double setLayoutY;

    @FXML private double layoutX;
    @FXML private double layoutY;

    public Paddle(){
        this.velocityX = 0;
    }

    public void setVel(double vel){
        this.velocityX = vel;
    }

    public void reset(){
        setLayoutX(100);
    }

    public void step() {
        this.setLayoutX = (this.getLayoutX() + this.velocityX);
    }
}


