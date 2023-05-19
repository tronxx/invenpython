 private function getPostResponse($uri, $data) {
      $client = new GuzzleHttp\Client(['base_uri' => $uri]);
      $options = ['headers' => [
        'Authorization' => "Token token=#{EMPRESA_API_KEY_PRIVADA}",
        'Accept'        => 'application/json',
        'Content-Type'  => 'application/json',
        'Access-Control-Allow-Origin' => '*'      
      ],'body' => json_encode($data)];
      
      $response = $client->request('POST', $uri, $options);
      $stream = Psr7\stream_for($response->getBody());
      return json_decode($stream, true);
    }
  