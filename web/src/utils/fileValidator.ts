export const validateLogFile = (file: File): { isValid: boolean; error?: string } => {
  const allowedExtensions = ['log', 'txt']
  const MAX_SIZE = 10 * 1024 * 1024 // 10MB
  const fileExtension = file.name.split('.').pop()?.toLowerCase()

  if (!fileExtension || !allowedExtensions.includes(fileExtension)) {
    return { isValid: false, error: 'Invalid file type. Please upload a .log or .txt file.' }
  }

  if (file.size > MAX_SIZE) {
    return { isValid: false, error: 'File is too large (Max 10MB).' }
  }

  return { isValid: true }
}
