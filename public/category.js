/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function Category(questionsListParam, titleParam)
{
    this.questionsList = questionsListParam;
    this.title = titleParam;
    this.currentQuestion = 0; // values: 0-4 (5 questions)
}

Category.prototype = {
    
};
