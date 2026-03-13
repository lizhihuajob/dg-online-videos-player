const isProduction = import.meta.env.PROD

const API_BASE = isProduction ? '/api' : 'http://localhost:8000'

export default API_BASE
