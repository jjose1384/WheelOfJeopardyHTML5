/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

function Category(questionsListParam, titleParam)
{
    this.questionsList = questionsListParam;
    this.title = titleParam;
    this.selectedQuestionIndex = 0; // values: 0-4 (5 questions)
    this.selectedQuestion = this.questionsList[0];
}

Category.prototype = {
    incrementSelectedQuestion: function()
    {
        var self = this;
        self.selectedQuestionIndex++;
        self.selectedQuestion = self.questionsList[self.selectedQuestionIndex];
    },
    
    // returns true if category is available, false otherwise
    isCategoryAvailable: function()
    {
        var self = this;
        if (self.selectedQuestionIndex <= 4)
        {
            return true;
        }
        
        return false;
    }
    
};
