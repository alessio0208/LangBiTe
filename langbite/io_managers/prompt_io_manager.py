import pandas
import numpy as np
from langbite.prompt import Prompt
from langbite.oracles import oracle_factory
import json

class PromptIOManager:

    RESPONSES_FILENAME = 'generated_responses'
    EVALUATIONS_FILENAME = 'generated_evaluations'
    GLOBAL_EVALUATION_FILENAME = 'global_evaluation'

    def load_prompts(self, prompts_path, languages):
        all_prompts = []
        for lang in languages:
            # reads a csv file containing the prompts, with the following columns:
            # - 0: prompt id
            # - 1: concern
            # - 2: prompt type
            # - 3: assessment type
            # - 4: task prefix
            # - 5: prompt template
            # - 6: output formatting instructions
            # - 7: oracle type
            # - 8: oracle prediction / evaluation expression
            # and appends the language code
            prompts_df = pandas.read_csv(prompts_path[lang], sep='\t')
            prompts_df = prompts_df.replace(np.nan, None)
            for value in prompts_df.values.tolist():
                prompt = Prompt(id=value[0],
                                concern=value[1],
                                input_type=value[2],
                                reflection_type=value[3],
                                task_prefix=value[4],
                                template=value[5],
                                output_formatting=value[6],
                                oracle=oracle_factory.factory.create(key=value[7],prediction=value[8],prompt_id=value[0]),
                                language=lang)
                all_prompts.append(prompt)
        return all_prompts
    
    def load_prompts_from_json(self, cases, input_language):
        all_prompts = []
        
        data = json.loads(cases)

        # Convert the dictionary to a DataFrame
        prompts_df = pandas.DataFrame(data)
        prompts_df = prompts_df.replace(np.nan, None)
        
        for value in prompts_df.values.tolist():
            prompt = Prompt(id=value[0],
                            concern=value[1],
                            input_type=value[2],
                            reflection_type=value[3],
                            task_prefix=value[4],
                            template=value[5],
                            output_formatting=value[6],
                            oracle=oracle_factory.factory.create(key=value[7],prediction=value[8],prompt_id=value[0]),
                            language=input_language)
            all_prompts.append(prompt)
            
        return all_prompts