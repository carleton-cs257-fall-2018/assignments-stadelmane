/**
 * Eric Stadelman and Charlie Broadbent
 * Controller.java
 * A class the performs all three of a model view and controller all in one
 */
package breakout;

import java.util.*;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;
import java.lang.Math;
import javafx.scene.layout.BackgroundFill;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

public class Controller implements EventHandler<KeyEvent> {
    final private double FRAMES_PER_SECOND = 45.0;

    @FXML private Button pauseButton;
    @FXML private Label scoreLabel;
    @FXML private Label livesLeft;
    @FXML private Label levelLabel;
    @FXML private Label startLabel;
    @FXML private AnchorPane gameBoard;
    @FXML private Paddle paddle;
    @FXML private Ball ball;
    @FXML private Rectangle leftWall;
    @FXML private Rectangle rightWall;
    @FXML private Rectangle bottomWall;
    @FXML private Rectangle topWall;

    ArrayList<Brick> listOfBricks;

    private int score;
    private boolean paused;
    private boolean startOfGame;
    private Timer timer;
    private int lives;
    private int level;

    public Controller() {
        this.paused = true;
        this.score = 0;
    }

    public void initialize() {
        startScreen();
        this.level = 0;
        endLevel();
        pause();
        this.livesLeft.setText(String.format("Lives left: %d", this.lives));
        this.scoreLabel.setText(String.format("Bricks Destroyed: %d", this.score));
    }

    //Controller
    /**
     * Moves the paddle if you press A or D on the keyboard
     * @param keyEvent either A or D key
     */
    public void handle(KeyEvent keyEvent) {
        KeyCode code = keyEvent.getCode();
        double paddlePosition = this.paddle.getLayoutX();
        double stepSize = 20.0;
        //if paused do not allow user to move paddle
        if (this.paused){
            keyEvent.consume();
        }
        else if (code == KeyCode.A) {
            // move paddle left
            if (paddlePosition > stepSize) {
                this.paddle.setLayoutX(this.paddle.getLayoutX() - stepSize);
            } else {
                this.paddle.setLayoutX(0);
            }
            keyEvent.consume();
        } else if (code == KeyCode.D) {
            // move paddle right
            if (paddlePosition + this.paddle.getWidth() + stepSize < this.gameBoard.
                    getWidth()) {
                this.paddle.setLayoutX(this.paddle.getLayoutX() + stepSize);
            } else {
                this.paddle.setLayoutX(this.gameBoard.getWidth() - this.paddle.
                        getWidth());
            }
            keyEvent.consume();
        }
    }

    //Model
    private void startTimer() {
        this.timer = new java.util.Timer();
        TimerTask timerTask = new TimerTask() {
            public void run() {
                Platform.runLater(new Runnable() {
                    public void run() {
                        updateAnimation();
                    }
                });
            }
        };
        long frameTimeInMilliseconds = (long)(1000.0 / FRAMES_PER_SECOND);
        this.timer.schedule(timerTask, 0, frameTimeInMilliseconds);
    }

    private void bounce(Rectangle rect){
        double ballVelocityX = this.ball.getVelocityX();
        double ballVelocityY = this.ball.getVelocityY();
        double ballCenterY = this.ball.getCenterY() + this.ball.getLayoutY();
        double ballCenterX = this.ball.getCenterX() + this.ball.getLayoutX();

        double rectTop = rect.getY() + rect.getLayoutY();
        double rectBottom = rect.getY() + rect.getLayoutY() + 25;
        double rectLeft = rect.getX() + rect.getLayoutX();
        double rectRight = rectLeft + rect.getWidth();

        //if rect is the paddle change ball x velocity based upon its distance from
        // the center of the paddle
        if (rect instanceof Paddle) {
            this.ball.setVelocityX(((Math.abs(ballCenterX - (rectLeft + 50)) / 10)+1
            )  * (this.ball.getVelocityX() / Math.abs(this.ball.getVelocityX())));
        }
        //cap velocity
        if (ballVelocityX > 9){
            this.ball.setVelocityX(9);
        }
        if (ballVelocityX < -9){
            this.ball.setVelocityX(-9);
        }
        //Checks to see if the ball hit the corner by checking which quartile of the
        // ball struck the rect
        if ((ballCenterX < rectLeft || ballCenterX > rectRight)){
            if ((ballCenterY < rectTop && ballVelocityY > 0 && ballCenterX
                    < rectLeft && ballVelocityX > 0) ||
                    (ballCenterY > rectBottom && ballVelocityY < 0 && ballCenterX
                            < rectLeft && ballVelocityX > 0) ||
                    (ballCenterY < rectTop && ballCenterX > rectRight &&
                            ballVelocityY > 0 && ballVelocityX < 0) ||
                    (ballCenterY < rectBottom && ballCenterX < rectRight &&
                            ballCenterY < 0 && ballVelocityX < 0)){
                this.ball.setVelocityX(-ballVelocityX);
                this.ball.setVelocityY(-this.ball.getVelocityY());
            }
            //Checks to see which direction the ball came from for top left corner.
            else if ((ballCenterY < rectTop && ballCenterX < rectLeft)) {
                if (ballVelocityY < 0) {
                    this.ball.setVelocityX(-ballVelocityX);
                } else {
                    this.ball.setVelocityY(-this.ball.getVelocityY());
                }
            }
            //top right corner
            else if (ballCenterY < rectTop && ballCenterX > rectRight){
                if(ballVelocityY < 0){
                    this.ball.setVelocityX(-ballVelocityX);
                }
                else{
                    this.ball.setVelocityY(-this.ball.getVelocityY());
                }
            }
            //bottom left corner
            else if ((ballCenterY > rectBottom && ballCenterX < rectLeft))
                if(ballVelocityY < 0){
                    this.ball.setVelocityY(-this.ball.getVelocityY());
                }
                else{
                    this.ball.setVelocityX(-this.ball.getVelocityX());
                }
            //bottom right
            else if ((ballCenterY > rectBottom && ballCenterX > rectRight)){
                if(ballVelocityY < 0){
                    this.ball.setVelocityY(-this.ball.getVelocityY());
                }
                else{
                    this.ball.setVelocityX(-this.ball.getVelocityX());
                }
            }
            //if in between top and bottom of rectangle switch X velocity because it
            // is hitting the side
            else if (ballCenterY > rectTop && ballCenterY < rectBottom){
                this.ball.setVelocityX(-ballVelocityX);
            }
        }
        //if hitting top or bottom switch Y velocity
        else{
            this.ball.setVelocityY(-this.ball.getVelocityY());
        }
    }

    private void updateAnimation() {
        double ballVelocityX = this.ball.getVelocityX();
        double ballVelocityY = this.ball.getVelocityY();

        //loop through every brick to check for collision
        for (Brick brick : this.listOfBricks) {
            if (ball.getBoundsInParent().intersects(brick.getBoundsInParent())) {
                if (brick.isDestroyed()) {
                } else {
                    this.bounce(brick);
                    brick.hit();
                    this.score++;
                    this.scoreLabel.setText(String.format("Bricks Destroyed: %d",
                            this.score));
                    if (brick.isDestroyed()) {
                        gameBoard.getChildren().remove(brick);
                    }
                    //if there are no bricks left (only walls paddle and ball)
                    if (gameBoard.getChildren().size() == 6){
                        endLevel();
                    }
                }
            }
        }
        if (ball.getBoundsInParent().intersects(this.paddle.getBoundsInParent())){
            this.bounce(paddle);
        }
        // Bounce off walls
        if (ball.getBoundsInParent().intersects(this.leftWall.getBoundsInParent())){
            this.ball.setVelocityX(-ballVelocityX);
        }
        if(ball.getBoundsInParent().intersects(this.rightWall.getBoundsInParent())){
            this.ball.setVelocityX(-ballVelocityX);
        }
        if (ball.getBoundsInParent().intersects(this.topWall.getBoundsInParent())){
            this.ball.setVelocityY(-ballVelocityY);
        }
        //if bottom wall lose life and reset
        if (ball.getBoundsInParent().intersects
                (this.bottomWall.getBoundsInParent())){
            this.lives--;
            this.reset();
        }
        this.ball.step();
    }

    private void endLevel(){
        level++;
        this.ball.reset();
        this.paddle.reset();
        this.levelLabel.setText(String.format("Level: %d", this.level));
        pause();

        //load new level using boolean matrix
        int columns = 0;
        int rows = 0;
        List<Boolean[]> list = new ArrayList<Boolean[]>();
        //test level
        if (level == 0){
            columns = 1;
            rows = 1;
            Boolean[] col1 = {true, false, false, false, false};
            list.add(col1);
        }

        if (level == 1){
            columns = 5;
            rows = 2;
            Boolean[] col1 = {true, true, true, true, true};
            Boolean[] col2 = {true, true, true, true, true};
            list.add(col1);
            list.add(col2);
        }
        if (level == 2) {
            columns = 5;
            rows = 8;
            //eyes
            Boolean[] col1 = {false, true, false, true, false};
            Boolean[] col2 = {false, true, false, true, false};

            //nose
            Boolean[] col4 = {false, false, true, false, false};

            //mouth
            Boolean[] col6 = {true, false, false, false, true};
            Boolean[] col7 = {false, true, false, true, false};
            Boolean[] col8 = {false, false, true, false, false};

            //empty space
            Boolean[] col3 = {false, false, false, false, false};
            Boolean[] col5 = {false, false, false, false, false};

            list.add(col1);
            list.add(col2);
            list.add(col3);
            list.add(col4);
            list.add(col5);
            list.add(col6);
            list.add(col7);
            list.add(col8);
            this.levelLabel.setText(String.format("Level :^)"));
        }
        if (level == 3) {
            columns = 5;
            rows = 8;
            Boolean[] col1 = {true, false, true, false, true};
            Boolean[] col2 = {true, false, true, false, false};
            Boolean[] col3 = {true, false, true, false, true};
            Boolean[] col4 = {true, true, true, false, true};
            Boolean[] col5 = {true, true, true, false, true};
            Boolean[] col6 = {true, false, true, false, true};
            Boolean[] col7 = {true, false, true, false, true};
            Boolean[] col8 = {true, false, true, false, true};

            list.add(col1);
            list.add(col2);
            list.add(col3);
            list.add(col4);
            list.add(col5);
            list.add(col6);
            list.add(col7);
            list.add(col8);

            this.levelLabel.setText(String.format("Level Hi"));
        }
        //if all levels are beat allow player to play as long as desired
        if (level >= 4){
            columns = 5;
            rows = 8;
            Boolean[] col1 = {true, true, true, true, true};
            Boolean[] col2 = {true, true, true, true, true};
            Boolean[] col3 = {true, true, true, true, true};
            Boolean[] col4 = {true, true, true, true, true};
            Boolean[] col5 = {true, true, true, true, true};
            Boolean[] col6 = {true, true, true, true, true};
            Boolean[] col7 = {true, true, true, true, true};
            Boolean[] col8 = {true, true, true, true, true};
            list.add(col1);
            list.add(col2);
            list.add(col3);
            list.add(col4);
            list.add(col5);
            list.add(col6);
            list.add(col7);
            list.add(col8);
        }
        startNewLevel(rows, columns, list);
    }


    //View
    private void startScreen(){
        this.startLabel.setText(String.format("To complete the level, destroy all "+
                "bricks without losing 3\n lives. Use A and D to move left and " +
                "right. The closer\n the ball strikes to the edges of the paddle the" +
                " faster it\n will bounce. Press the Start button begin"));
        this.startLabel.setTextFill(Color.WHITE);
        this.startLabel.setBackground(new Background(new BackgroundFill(Color.BLACK,
                CornerRadii.EMPTY, Insets.EMPTY)));
        this.startOfGame = true;
    }

    private void startNewLevel(int rows , int columns , List<Boolean[]> list){
        lives = 3;
        this.livesLeft.setText(String.format("Lives left: %d", this.lives));
        this.listOfBricks = new ArrayList<Brick>();
        //loops through boolean matrix to draw brick design
        for (int i = 0; i < columns; ++i) {
            for (int j = 0; j < rows; ++j) {
                if (list.get(j)[i]) {
                    Brick brickToAdd = new Brick(i, j);
                    this.gameBoard.getChildren().add(brickToAdd);
                    listOfBricks.add(brickToAdd);
                }
            }
        }
    }



    //Aspects of both model and view
    private void pause(){
        {
            if (this.paused) {
                this.pauseButton.setText("Pause");
                this.startTimer();
            } else {
                this.pauseButton.setText("Start");
                this.timer.cancel();
            }
            this.paused = !this.paused;
        }
    }

    /**
     * Pauses and unpauses the game by stopping or starting the timer when
     * the Start/Pause button is clicked
     * @param actionEvent click on the button
     */
    public void onPauseButton(ActionEvent actionEvent) {
        if (this.startOfGame){
            this.startOfGame = false;
            gameBoard.getChildren().remove(this.startLabel);
        }
        if (this.paused) {
            this.pauseButton.setText("Pause");
            this.startTimer();
        } else {
            this.pauseButton.setText("Start");
            this.timer.cancel();
        }
        this.paused = !this.paused;
    }

    private void reset() {
        this.levelLabel.setText(String.format("Level: %d", this.level));
        if (lives == 0){
            for (Brick brick : this.listOfBricks) {
                gameBoard.getChildren().remove(brick);
            }
            lives = 3;
            this.level = 0;
            this.score = 0;
            endLevel();
            reset();
        }
        else {
            this.pauseButton.setText("Start");
            this.timer.cancel();
            this.ball.reset();
            this.paddle.reset();
            this.paused = !this.paused;
        }
        this.scoreLabel.setText(String.format("Bricks Destroyed: %d", this.score));
        this.livesLeft.setText(String.format("Lives left: %d", this.lives));
    }
}