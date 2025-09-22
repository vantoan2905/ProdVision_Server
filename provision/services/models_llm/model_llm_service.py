import requests
from transformers import AutoModelForCausalLM, AutoTokenizer

class ModelLLMService_API:
    def __init__(self, model_name, api_key, api_url, api_version=None, api_type=None,
                 max_tokens=512, temperature=0.7, top_p=1.0, n=1, stream=False, stop=None):
        """
        Initialize ModelLLMService_API.

        Parameters
        ----------
        model_name : str
            Name of the pre-trained model.
        api_key : str
            API key for accessing the model.
        api_url : str
            URL of the API endpoint.
        api_version : str, optional
            Version of the API.
        api_type : str, optional
            Type of the API.
        max_tokens : int, optional
            Maximum number of tokens to generate.
        temperature : float, optional
            Temperature for generating tokens.
        top_p : float, optional
            Top p value for generating tokens.
        n : int, optional
            Number of generated tokens.
        stream : bool, optional
            Whether to stream the generated tokens.
        stop : str or list of str, optional
            Tokens to stop generating at.
        """

        self.model_name = model_name
        self.api_key = api_key
        self.api_url = api_url
        self.api_version = api_version
        self.api_type = api_type
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop

    def generate_response(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "n": self.n,
            "stream": self.stream,
            "stop": self.stop
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()


class ModelLLMService_Local:
    def __init__(self, model_name, model_version=None,
                 max_tokens=512, temperature=0.7, top_p=1.0, n=1, stream=False, stop=None):
        """
        Initialize ModelLLMService_Local.

        Parameters
        ----------
        model_name : str
            Name of the pre-trained model.
        model_version : str, optional
            Version of the pre-trained model.
        max_tokens : int, optional
            Maximum number of tokens to generate.
        temperature : float, optional
            Temperature for generating tokens.
        top_p : float, optional
            Top p value for generating tokens.
        n : int, optional
            Number of generated tokens.
        stream : bool, optional
            Whether to stream the generated tokens.
        stop : str or list of str, optional
            Tokens to stop generating at.

        Attributes
        ----------
        tokenizer : transformers.AutoTokenizer
            Tokenizer for the pre-trained model.
        model : transformers.AutoModelForCausalLM
            Pre-trained model for causal language modeling.
        """
        self.model_name = model_name
        self.model_version = model_version
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            num_return_sequences=self.n
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
